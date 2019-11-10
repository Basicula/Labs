let DATABASES = [];
let MONGO_DATABASES = [];
let TABLES = [];
let TABLE = [];
const MSG = $('#message');
const DB_TABLE = $('#db-table');
const DB_NAV = $('#databases');
const DB_MONGO_NAV = $('#mongo-databases');
const TABLES_NAV = $('#tables');
const CREATE_DATABASE_POPUP = $('#create-database-popup');
const CREATE_TABLE_POPUP = $('#create-table-popup');
const MERGE_TABLES_POPUP = $('#merge-tables-popup');
const CONTENT = $('.content');
const ENTERED_NAME = $('input[name=name]');
const ENTERED_TABLE_NAME = $('input[name=table-name]');
const SCHEME = $('#scheme');
let CURRENT_DB_INDEX = -1;
let CURRENT_TABLE_INDEX = -1;
let MONGO = false;


function detect_database() {
    if (CURRENT_DB_INDEX < DATABASES.length)
        return DATABASES[CURRENT_DB_INDEX]
    else
        return MONGO_DATABASES[CURRENT_DB_INDEX-DATABASES.length]
}

function update_tables() {
    if (CURRENT_DB_INDEX === -1) {
        TABLES = [];
        return;
    }
    select_table(-1);
    $.get('/databases/' + detect_database() + '/tables', function (response) {
        if (response.status === 'OK') {
            TABLES = response.result;
            TABLES_NAV.text('');
            for (let i = 0; i < TABLES.length; i++) {
                const table_btn = $('<a onClick="select_table(' + i + ')" id="table_' + i + '"></a>');
                table_btn.text(TABLES[i]);
                TABLES_NAV.append(table_btn);
            }
            if (TABLES.length > 0) select_table(0);
            display_status(response.status, 'Tables loaded');
        } else {
            display_status(response.status, response.message);
        }
    });
}

function update_databases() {
    select_db(-1);
    $.get('/databases', function (response) {
        if (response.status === 'OK') {
            let k = 0;
            DATABASES = response.result.local;
            DB_NAV.text('');
            for (let i = 0; i < DATABASES.length; i++) {
                const del_button = $('<div class="delete" onclick="delete_database(' + i + ')">X</div>');
                const db_row = $('<li onClick="select_db(' + i + ')" id="db_' + i + '" class="row"></li>');
                db_row.text(DATABASES[i]);
                db_row.append(del_button);
                DB_NAV.append(db_row);
                k++;
            }
            
            MONGO_DATABASES = response.result.mongo;
            DB_MONGO_NAV.text('');
            for (let i = 0; i < MONGO_DATABASES.length; i++) {
                const del_button = $('<div class="delete" onclick="delete_mongo_database(' + i + ')">X</div>');
                const db_row = $('<li onClick="select_db(' + k + ')" id="db_' + k + '" class="row"></li>');
                db_row.text(MONGO_DATABASES[i]);
                db_row.append(del_button);
                DB_MONGO_NAV.append(db_row);
                k++;
            }
            
            if (DATABASES.length + MONGO_DATABASES.length > 0) select_db(0);
            display_status(response.status, 'Databases loaded');
        } else {
            display_status(response.status, response.message);
        }
    });
}

function select_db(db_index) {
    if (CURRENT_DB_INDEX !== db_index) {
        if (CURRENT_DB_INDEX !== -1) {
            const prev = $('#db_' + CURRENT_DB_INDEX);
            prev.removeClass('active');
        }
        select_table(-1);
        CURRENT_DB_INDEX = db_index;
        if (db_index !== -1) {
            update_tables();
            const next = $('#db_' + db_index);
            next.addClass('active');
        }
    }
}

function select_table(table_index) {
    //if (CURRENT_TABLE_INDEX !== table_index) {
    if (CURRENT_TABLE_INDEX !== -1) {
        const prev = $('#table_' + CURRENT_TABLE_INDEX);
        prev.removeClass('active');
    }
    CURRENT_TABLE_INDEX = table_index;
    update_table();
    if (table_index !== -1) {
        const next = $('#table_' + table_index);
        next.addClass('active');
    }
    //}
}

function build_table(editable = false) {
    DB_TABLE.html('');
    let row = $('<tr></tr>');
    for (let i = 0; i < TABLE.columns.length; i++) {
        let col = TABLE.columns[i];
        row.append($('<td>' + col.header + '</td>'));
    }
    row.append($('<td></td>'));
    DB_TABLE.append(row);
    for (let i = 0; i < TABLE.rows.length; i++) {
        let row = $('<tr></tr>');
        for (let j = 0; j < TABLE.rows[i].length; j++) {
            let cell = $('<td></td>');
            if (TABLE.columns[j].type === 'picture') {
                cell.text('🖼' + TABLE.rows[i][j]);
                cell.append('<img class="popup-image" src="' + storage_url + 'download/' + TABLE.rows[i][j] + '">');
            } else {
                cell.text(TABLE.rows[i][j].data);
            }
            row.append(cell);
        }
        if (editable)
            row.append($('<td onClick="delete_row(' + i + ')" class="delete">X</td>'));
        DB_TABLE.append(row);
    }

    if (editable) {
        row = $('<tr></tr>');
        for (let i = 0; i < TABLE.columns.length; i++) {
                const cell = $('<td></td>');
            if (TABLE.columns[i].type === 'picture') {
                const dropdown = $('<div class="dropdown-head"></div>');
                dropdown.append($('<a>⬇⬇⬇Select image</a>'));
                dropdown.append($('<div class="dropdown-content" id="images"></div>'));
                $.get('/files', function(response){
                    if (response.status === 'OK') {
                        console.log(response);
                        const images = $('#images');
                        response.result.forEach(function(file) {
                            const a = $('<div onclick="select_image(this, \'value_'+TABLE.columns[i].header+'\',\''+file+'\')"></div>');
                            a.text(file);
                            images.append(a);
                        });
                    }
                });
                cell.append($('<input type="text" id="value_' + TABLE.columns[i].header + '" hidden>'));
                cell.append(dropdown);
            } else {
                cell.append($('<input type="text" id="value_' + TABLE.columns[i].header + '" class="row-value">'));
            }
                row.append(cell);
        }
        row.append($('<td onClick="create_row()">+</td>'));
        DB_TABLE.append(row);
    }
}

function select_image(e, value_id, name) {
    console.log(e);
    $('.dropdown-content div').removeClass('active');
    $(e).addClass('active');
    $('#'+value_id).attr('value', name);
    $('.dropdown-head > a').text('⬇⬇⬇'+name);
}

function update_table() {
    if (CURRENT_TABLE_INDEX === -1) {
        MSG.show();
        DB_TABLE.html('');
        return;
    }
    MSG.hide();
    $.get('/databases/' + detect_database() + '/tables/' + TABLES[CURRENT_TABLE_INDEX], function (response) {
        if (response.status === 'OK') {
            TABLE = response['result'];
            build_table(true);
            display_status(response.status, 'Table "' + TABLES[CURRENT_TABLE_INDEX] + '" loaded');
        } else {
            display_status(response.status, response.message);
        }
    });
}

function delete_row(row_index) {
    $.ajax({
        url: '/databases/' + detect_database() + '/tables/' + TABLES[CURRENT_TABLE_INDEX] + '/rows',
        type: 'DELETE',
        data: {index: row_index},
        success: function (response) {
            display_status(response.status, response.message);
            update_table();
        }
    });
}

function delete_table() {
    if (CURRENT_TABLE_INDEX !== -1 && CURRENT_DB_INDEX !== -1) {
        $.ajax({
            url: '/databases/' + detect_database() + '/tables/' + TABLES[CURRENT_TABLE_INDEX],
            type: 'DELETE',
            success: function (response) {
                display_status(response.status, response.message);
                update_tables();
            }
        });
    }
}

function delete_database() {
    if (CURRENT_DB_INDEX !== -1) {
        $.ajax({
            url: '/databases/' + detect_database(),
            type: 'DELETE',
            success: function (response) {
                display_status(response.status, response.message);
                update_databases();
            }
        });
    }
}

function create_row() {
    let cells = [];
    for (let i = 0; i < TABLE.columns.length; i++) {
        cells.push($('#value_' + TABLE.columns[i].header).val())
    }
    $.post('/databases/' + detect_database() + '/tables/' + TABLES[CURRENT_TABLE_INDEX] + '/row',
        {
            cells: cells
        },
        function (response) {
            display_status(response.status, response.message);
            update_table();
        });
}

function create_database(db_name, mongo) {
    if (db_name) {
        $.post('/databases', {db_name: db_name, mongo: mongo}, function (response) {
            display_status(response.status, response.message);
            update_databases();
        });
    } else {
        show_database_popup();
    }
}

function create_click() {
    create_database(ENTERED_NAME.val(), $('#mongodb').prop("checked"));
    hide_database_popup();
}

function create_table(table_name, types, headers) {
    if (table_name) {
        console.log(types);
        console.log(headers);
        $.post('/databases/' + detect_database() + '/tables', {name: table_name, types: types, headers: headers},
            function (response) {
                display_status(response.status, response.message);
                update_tables();
            });
    } else {
        show_table_popup();
    }
}

function create_table_click() {
    let types = [];
    let names = [];
    let columns = SCHEME.find('.column');
    for (let i = 0; i < columns.length; i++) {
        const o = $(columns[i]);
        let type = o.find('.type').text();
        const name = o.find('input').val();
        switch (type) {
            case "Real":
                type = "real";
                break;
            case "Int":
                type = "integer";
                break;
            case "Str":
                type = "string";
                break;
            case "Chr":
                type = "char";
                break;
            case "Img":
                type = "picture";
                break;
        }
        types.push(type);
        names.push(name);
    }
    create_table(ENTERED_TABLE_NAME.val(), types, names);
    hide_table_popup();
}

const log = $('#log');
log.html('');

function display_status(status, message) {
    const status_message = $('<div class="status"></div>');
    if (status === 'OK') status_message.addClass('ok');
    if (status === 'ERROR') status_message.addClass('error');
    if (message) {
        status_message.html(status + ': ' + message);
    } else {
        status_message.html(status);
    }
    log.append(status_message);
}

setInterval(function () {
    const messages = $('.status');
    for (let i = 0; i < messages.length; i++) {
        const status_message = $(messages[i]);
        const opacity = status_message.css('opacity');
        status_message.css('opacity', opacity - 0.005);
        if (opacity < 0.01) status_message.remove();
    }
}, 100);

function show_database_popup() {
    CONTENT.css('opacity', 0.3);
    CREATE_DATABASE_POPUP.show();
    ENTERED_NAME.focus();
}

function hide_database_popup() {
    CONTENT.css('opacity', 1.0);
    CREATE_DATABASE_POPUP.hide();
}

function show_table_popup() {
    CONTENT.css('opacity', 0.3);
    CREATE_TABLE_POPUP.show();
    ENTERED_TABLE_NAME.focus();
    SCHEME.html('');
    add_column('Int', 'id');
}

function hide_table_popup() {
    CONTENT.css('opacity', 1.0);
    CREATE_TABLE_POPUP.hide();
}

function show_merge_popup() {
    CONTENT.css('opacity', 0.3);
    MERGE_TABLES_POPUP.show();
    SCHEME.html('');

    const tables_to_merge = $('#tables-to-merge');
    tables_to_merge.html('');
    $.get('/databases/' + detect_database() + '/tables', function (response) {
        if (response.status === 'OK') {
            response.result.forEach(function (table) {
                tables_to_merge.append($('<div class="row" onclick="select_table_to_merge(this)">' + table + '</div>'));
            });
            select_table_to_merge(tables_to_merge.children().first());
        }
    });
}

function click_merge() {
    const active_tables = $('#tables-to-merge').children();
    let tables = [];
    for (let i = 0;i<active_tables.length;i++) {
        if($(active_tables[i]).hasClass('active'))
            tables.push($(active_tables[i]).text());
    }
    merge_tables(
        tables,
        $('input[name=as]').val()
    );
    hide_merge_popup();
}

function select_table_to_merge(e) {
    if ($(e).hasClass('active'))
        $(e).removeClass('active');
    else
        $(e).addClass('active');
}

function hide_merge_popup() {
    CONTENT.css('opacity', 1.0);
    MERGE_TABLES_POPUP.hide();
}

function merge_tables(tables, new_name) {
    console.log(tables, new_name);
    if (tables.length > 1) {
        let table1 = TABLES[CURRENT_TABLE_INDEX];
        $.post('/databases/' + detect_database() + '/mergetables', {tables : tables, new_name : new_name}, function (response) {
            if (response.status === 'OK') {
                update_tables()
                display_status(response.status, response.message);
            } else {
                display_status(response.status, response.message);
            }
        });
    } else {
        show_merge_popup();
    }
}

function add_column(type, name = 'column') {
    const column = $('<div class="column"></div>');
    column.append($('<div class="type">' + type + '</div>'));
    column.append($('<input type="text" value="' + name + '">'));
    column.append($('<div class="remove" onclick="$(this.parentElement).remove()">X</div>'));
    SCHEME.append(column);
}

update_databases();
update_tables();
update_table();