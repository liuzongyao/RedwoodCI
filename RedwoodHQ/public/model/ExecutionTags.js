Ext.define('Redwood.model.ExecutionTags', {
    extend: 'Ext.data.Model',
    idProperty: '_id',

    fields: [
        {
            name: 'value',
            type: 'string'
        }, {
            name: '_id',
            type: 'string'
        }]
});